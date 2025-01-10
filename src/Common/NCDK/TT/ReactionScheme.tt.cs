



// .NET Framework port by Kazuya Ujihara
// Copyright (C) 2016-2017  Kazuya Ujihara <ujihara.kazuya@gmail.com>

/* Copyright (C) 2006-2007  Miguel Rojas <miguelrojasch@yahoo.es>
 *
 *  Contact: cdk-devel@lists.sourceforge.net
 *
 *  This program is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU Lesser General Public License
 *  as published by the Free Software Foundation; either version 2.1
 *  of the License, or (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT Any WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Lesser General Public License for more details.
 *
 *  You should have received a copy of the GNU Lesser General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA.
 */

using System.Collections.Generic;

namespace NCDK.Default
{
    /// <summary>
    /// Classes that : the definition of reaction to a scheme.
    /// This is designed to contain a set of reactions which are linked in
    /// some way but without hard coded semantics.
    /// </summary>
    // @author      miguelrojasch <miguelrojasch@yahoo.es>
    public class ReactionScheme 
        : ReactionSet, IReactionScheme
    {
        /// <summary>
        /// A List of reaction schemes
        /// </summary>
        private List<IReactionScheme> reactionScheme;

        /// <summary>
        /// Constructs an empty ReactionScheme.
        /// </summary>
        public ReactionScheme()
        {
            reactionScheme = new List<IReactionScheme>();
        }

        /// <inheritdoc/>
        public void Add(IReactionScheme scheme)
        {
            reactionScheme.Add(scheme);
        }

        /// <inheritdoc/>
        public ICollection<IReactionScheme> Schemes => reactionScheme;

        /// <inheritdoc/>
        public void Remove(IReactionScheme scheme)
        {
            reactionScheme.Remove(scheme);
        }

        /// <inheritdoc/>
        public IEnumerable<IReaction> Reactions => this;

        /// <inheritdoc/>
        public override ICDKObject Clone(CDKObjectMap map)
        {
            var reactionScheme = new List<IReactionScheme>();
            foreach (var scheme in Schemes)
            {
                reactionScheme.Add((IReactionScheme)scheme.Clone(map));
            }
            ReactionScheme clone = (ReactionScheme)base.Clone(map);
            clone.reactionScheme = reactionScheme;
            return clone;
        }
    }
}
namespace NCDK.Silent
{
    /// <summary>
    /// Classes that : the definition of reaction to a scheme.
    /// This is designed to contain a set of reactions which are linked in
    /// some way but without hard coded semantics.
    /// </summary>
    // @author      miguelrojasch <miguelrojasch@yahoo.es>
    public class ReactionScheme 
        : ReactionSet, IReactionScheme
    {
        /// <summary>
        /// A List of reaction schemes
        /// </summary>
        private List<IReactionScheme> reactionScheme;

        /// <summary>
        /// Constructs an empty ReactionScheme.
        /// </summary>
        public ReactionScheme()
        {
            reactionScheme = new List<IReactionScheme>();
        }

        /// <inheritdoc/>
        public void Add(IReactionScheme scheme)
        {
            reactionScheme.Add(scheme);
        }

        /// <inheritdoc/>
        public ICollection<IReactionScheme> Schemes => reactionScheme;

        /// <inheritdoc/>
        public void Remove(IReactionScheme scheme)
        {
            reactionScheme.Remove(scheme);
        }

        /// <inheritdoc/>
        public IEnumerable<IReaction> Reactions => this;

        /// <inheritdoc/>
        public override ICDKObject Clone(CDKObjectMap map)
        {
            var reactionScheme = new List<IReactionScheme>();
            foreach (var scheme in Schemes)
            {
                reactionScheme.Add((IReactionScheme)scheme.Clone(map));
            }
            ReactionScheme clone = (ReactionScheme)base.Clone(map);
            clone.reactionScheme = reactionScheme;
            return clone;
        }
    }
}

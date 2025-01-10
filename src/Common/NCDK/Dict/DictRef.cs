/* Copyright (C) 2003-2008  Egon Willighagen <egonw@users.sf.net>
 *
 * Contact: cdk-devel@lists.sourceforge.net
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public License
 * as published by the Free Software Foundation; either version 2.1
 * of the License, or (at your option) any later version.
 * All we ask is that proper credit is given for our work, which includes
 * - but is not limited to - adding the above copyright notice to the beginning
 * of your source code files, and to any copyright notice that you may distribute
 * with programs based on this work.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT Any WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA.
 */

using System;

namespace NCDK.Dict
{
    /// <summary>
    /// Object that can be used as key in IChemObject.SetProperty(key, value) to
    /// denote that this property is a dictionary reference for this IChemObject.
    /// </summary>
    // @author      Egon Willighagen
    // @cdk.created 2003-08-24
    // @cdk.module  standard
    public class DictRef
    {
        readonly string type;
        readonly string reference;

        public DictRef(string type, string dictRef)
        {
            this.type = type;
            this.reference = dictRef;
        }

        public string Reference => reference;

        public string Type => type;

        public override string ToString()
        {
            return "DictRef{T=" + this.type + ", R=" + reference + "}";
        }

        public virtual DictRef Clone()
        {
            return (DictRef)this.MemberwiseClone();
        }
    }
}

/* Copyright (C) 1997-2007  The Chemistry Development Kit (CDK) project
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

namespace NCDK.IO
{
    /// <summary>
    /// This class is the interface that all IO writers should implement.
    /// Programs need only care about this interface for any kind of IO.
    /// <para>
    /// Currently, database IO and file IO is supported. Internet IO is expected.</para>
    /// </summary>
    // @cdk.module io
    public interface IChemObjectWriter : IChemObjectIO
    {
        /// <summary>
        /// Writes the content of "object" to output.
        /// </summary>
        /// <param name="o">the object of which the content is outputted</param>
        /// <exception cref="CDKException">is thrown if the output does not support the data in the object</exception>
        void Write(IChemObject o);
    }
}
